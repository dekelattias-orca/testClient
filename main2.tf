resource "aws_instance" "host" {
  ami           = "ami-0ddb05e945a674cf5" # Example AMI ID, use a valid one
  instance_type = "t2.micro"

  # Require IMDSv2
  metadata_options {
    http_tokens = "required"
    http_endpoint = "enabled"
    http_put_response_hop_limit = 1 # Default, but can be set higher if needed
  }
}
