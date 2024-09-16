from aws_cdk import (
    aws_ec2 as ec2,
    App, Stack, Environment
)

class MyEc2Stack(Stack):
    def __init__(self, scope: App, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)


        security_group = ec2.SecurityGroup(
            self,
            "InstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Permitir tráfico SSH y HTTP desde cualquier lugar"
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP")


        ec2.Instance(
            self,
            "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": "ami-049d6539112c3246e"}),
            vpc=vpc,
            key_name="vockey",
            security_group=security_group
        )



app = App()
MyEc2Stack(app, "MyEc2Stack", env=Environment(account="522813847784", region="us-east-1"))
app.synth()
