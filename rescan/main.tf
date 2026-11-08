resource "aws_s3_bucket" "logs" {
  bucket = "spike-logs"
  acl    = "public-read"
}

resource "aws_s3_bucket" "data" {
  bucket = "spike-data"
}

resource "aws_s3_bucket_ownership_controls" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "data" {
  depends_on = [aws_s3_bucket_ownership_controls.data]

  bucket = aws_s3_bucket.data.id
  acl    = "private"
}
