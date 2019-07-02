# CodeBuild
#
resource "aws_iam_role" "build" {
  name = "build"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "build" {
  role = "${aws_iam_role.build.name}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeSubnets",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs"
      ],
      "Resource": "*"
    }
  ]
}
POLICY
}

resource "aws_codebuild_project" "build" {
  name          = "trending"
  description   = "Trending CodeBuild project"
  build_timeout = "5"
  service_role  = "${aws_iam_role.build.arn}"

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:2.0"
    type         = "LINUX_CONTAINER"
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/ffung/trending.git"
    git_clone_depth = 1
  }

  vpc_config {
    vpc_id = "${var.vpc_id}"
    subnets = "${var.subnets}"
    security_group_ids = [
      "${var.security_group_id}"
    ]
  }

  tags = {
    Environment = "Test"
  }
}

resource "aws_codebuild_webhook" "build" {
  project_name = "${aws_codebuild_project.build.name}"

}

resource "github_repository_webhook" "build" {
  active     = true
  events     = ["push"]
  repository = "${var.github_repository_name"}"

  configuration {
    url          = "${aws_codebuild_webhook.build.payload_url}"
    secret       = "${aws_codebuild_webhook.build.secret}"
    content_type = "json"
    insecure_ssl = false
  }
}
