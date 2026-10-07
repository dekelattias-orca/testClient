# storage.tf — CASE 2: IaC findings, to exercise the IaC persona.
#
# The IaC persona licenses ADDING resources where the SAST one forbids
# inventing code, so a correct fix here may introduce a new block rather than
# only edit an attribute. Expectation: FIXED.

resource "aws_s3_bucket" "reports" {
  bucket = "shiftleft-prfix-eval-reports"
}

# Object ownership controls so the ACL below is accepted by S3.
resource "aws_s3_bucket_ownership_controls" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    object_ownership = "ObjectWriter"
  }
}

# Private ACL — no anonymous read or write access.
resource "aws_s3_bucket_acl" "reports" {
  bucket = aws_s3_bucket.reports.id
  acl    = "private"

  depends_on = [aws_s3_bucket_ownership_controls.reports]
}

# Block any public ACL or public bucket policy from being applied later.
resource "aws_s3_bucket_public_access_block" "reports" {
  bucket = aws_s3_bucket.reports.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

variable "admin_ingress_cidrs" {
  description = "Trusted CIDR blocks (e.g. VPN or bastion ranges) permitted to reach the admin shell port of the reports service."
  type        = list(string)

  validation {
    condition = length(var.admin_ingress_cidrs) > 0 && length([
      for cidr in var.admin_ingress_cidrs : cidr
      if cidr == "0.0.0.0/0" || cidr == "::/0"
    ]) == 0
    error_message = "admin_ingress_cidrs must be non-empty and must not allow unrestricted access from the internet."
  }
}

resource "aws_security_group" "reports_ingress" {
  name        = "reports-ingress"
  description = "Ingress for the reports service"

  # Admin shell access is limited to explicitly trusted CIDR ranges.
  ingress {
    description = "admin shell access from trusted networks only"
    from_port   = 2222
    to_port     = 2222
    protocol    = "tcp"
    self        = false
    cidr_blocks = var.admin_ingress_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_sqs_queue" "code_ops_static_ip_queue" {
  name                        = local.static_ip_queue_name
  fifo_queue                  = true
  content_based_deduplication = false # producers set MessageDeduplicationId = request_id
  visibility_timeout_seconds  = 60
  sqs_managed_sse_enabled     = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.code_ops_static_ip_deadletter_queue.arn
    maxReceiveCount     = 4
  })
  tags = {
    environment = var.env_name
    team        = "appsec-team"
    app         = "shiftleft-code-ops"
  }
}
