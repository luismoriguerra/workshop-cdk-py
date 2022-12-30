from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
)

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ################ Fargate example 2 ################
        self.vpc = ec2.Vpc(self, "lgpy-vpc", max_azs=2)
        self.cluster = ecs.Cluster(self, "lgpy-cluster", vpc=self.vpc)
        webdocker = ecr_assets.DockerImageAsset(self, "lgpy-api-test", directory="./server")

        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "lgpy-fargate-service-2",
            cluster=self.cluster,
            # container image
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(webdocker),
                container_port=5000,
            )
        )

        self.service.target_group.configure_health_check(
            path='/health'
        )

        ################ Fargate example 2 ################

        ################ Fargate example ################
        # # create vpc
        # self.vpc = ec2.Vpc(self, "lgpy-vpc", max_azs=2)
        # self.cluster = ecs.Cluster(self, "lgpy-cluster", vpc=self.vpc)

        # # initiate fargate service
        # self.fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
        #     self, "lgpy-fargate-service",
        #     cluster=self.cluster,
        #     task_image_options={
        #         "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        #     }
        # )

        ########################################

        # my_lambda = _lambda.Function(
        #     self, 'lgpy-lambda',
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     code=_lambda.Code.from_asset('lambda'),
        #     handler='hello.handler',
        # )

        # hello_with_counter = HitCounter(
        #     self, 'HelloHitCounter',
        #     downstreamFn=my_lambda,
        # )

        # apigw.LambdaRestApi(
        #     self, 'LGEndpoint',
        #     handler=hello_with_counter.handler,
        # )

        # TableViewer(
        #     self, 'LGViewHitCounter',
        #     title='Hello Hits',
        #     table=hello_with_counter.table,
        # )
