resource "aws_s3_bucket" "logs" {
  bucket = "spike-logs"
  acl    = "public-read"
}

resource "aws_s3_bucket" "data" {
  bucket = "spike-data"
  acl    = "public-read"
}
