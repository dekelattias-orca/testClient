# IaC false positive: an internal queue, encryption handled by the account default.
# (retrigger)
resource "aws_sqs_queue" "internal_jobs" {
  name = "internal-jobs"
}
