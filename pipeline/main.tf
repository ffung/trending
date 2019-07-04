
resource "aws_s3_bucket" "build" {
  bucket = "trending-bucket"
}

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
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterfacePermission"
      ],
      "Resource": "arn:aws:ec2:${var.region}:${var.account_id}:network-interface/*",
      "Condition": {
         "StringEquals": {
             "ec2:Subnet": [
               "arn:aws:ec2:${var.region}:${var.account_id}:subnet/${var.subnets[0]}"
             ],
             "ec2:AuthorizedService": "codebuild.amazonaws.com"
         }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.build.arn}",
        "${aws_s3_bucket.build.arn}/*"
      ]
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
    type = "S3"
    location = "${aws_s3_bucket.build.bucket}"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:2.0"
    type         = "LINUX_CONTAINER"
  }

  source {
    type            = "GITHUB"
    location        = "${var.github_repository}"
    git_clone_depth = 1
  }

  vpc_config {
    vpc_id = "${var.vpc_id}"
    subnets = ["${var.subnets[0]}"]
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
