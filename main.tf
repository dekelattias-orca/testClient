 resource "aws_instance" "infra" {
   depends_on                  = [module.vpc]
   for_each                    = var.ec2_describe
   ami                         = data.aws_ami.debian_image.image_id
   instance_type               = each.value.instance_type
   private_ip                  = each.value.private_ip
   root_block_device {
     delete_on_termination = true
     encrypted             = false
     volume_size           = 120
     volume_type           = "gp3"
   }
   metadata_options {
     http_endpoint = "enabled"
     http_tokens   = "optional"
   }
 }
resource "aws_sqs_queue" "code_ops_static_ip_queue" {
name = local.static_ip_queue_name
fifo_queue = true
content_based_deduplication = false # producers set MessageDeduplicationId = request_id
visibility_timeout_seconds = 60
sqs_managed_sse_enabled = true
redrive_policy = jsonencode({
deadLetterTargetArn = aws_sqs_queue.code_ops_static_ip_deadletter_queue.arn
maxReceiveCount = 4
})
tags = {
environment = var.env_name
team = "appsec-team"
app = "shiftleft-code-ops"
}
}
