# IaC false positive: an internal queue, encryption handled by the account default.
resource "aws_sqs_queue" "internal_jobs" {
  name = "internal-jobs"
}
