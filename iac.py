from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class MyEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
                                           vpc=vpc,
                                           security_group_name="AllowSSH_HTTP",
                                           description="Permitir tráfico SSH y HTTP desde cualquier lugar",
                                           allow_all_outbound=True
                                           )

        # Permitir tráfico SSH y HTTP
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH desde cualquier lugar")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP desde cualquier lugar")

        # Configurar la instancia EC2
        instance = ec2.Instance(self, "MyInstance",
                                instance_type=ec2.InstanceType("t2.micro"),
                                machine_image=ec2.MachineImage.generic_linux({"us-east-1": "ami-049d6539112c3246e"}),
                                vpc=vpc,
                                key_name="vockey",
                                security_group=security_group
                                )

        instance.user_data.add_commands(
            "sudo yum update -y",
            "sudo yum install -y httpd",
            "sudo systemctl start httpd",
            "sudo systemctl enable httpd",
            "cd /var/www/html",
            "git clone https://github.com/edson123450/websimple.git",
            "git clone https://github.com/edson123450/webplantilla.git"
        )
app = core.App()
MyEc2Stack(app, "MyEc2Stack")
app.synth()