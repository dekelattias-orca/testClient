# storage.tf — CASE 2: IaC findings, to exercise the IaC persona.
#
# The IaC persona licenses ADDING resources where the SAST one forbids
# inventing code, so a correct fix here may introduce a new block rather than
# only edit an attribute. Expectation: FIXED.

resource "aws_s3_bucket" "reports" {
  bucket = "shiftleft-prfix-eval-reports"
}

# Unencrypted at rest, world-readable ACL, no public-access block.
resource "aws_s3_bucket_acl" "reports" {
  bucket = aws_s3_bucket.reports.id
  acl    = "public-read"
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
