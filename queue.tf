# Rebuild queue for the docs site. Nothing here stores objects — the only S3 in
# this stack is the published-docs bucket, which is public on purpose.
resource "aws_sqs_queue" "docs_rebuild" {
  name                        = "docs-rebuild.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  sqs_managed_sse_enabled     = true
}
