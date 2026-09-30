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

resource "aws_security_group" "reports_ingress" {
  name        = "reports-ingress"
  description = "Ingress for the reports service"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
