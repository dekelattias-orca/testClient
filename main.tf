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
