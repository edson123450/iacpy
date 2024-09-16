import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export class MyEc2Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 2,
    });


    const securityGroup = new ec2.SecurityGroup(this, 'InstanceSecurityGroup', {
      vpc,
      allowAllOutbound: true,
      description: 'Permitir tráfico SSH y HTTP desde cualquier lugar',
    });

    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'Permitir SSH');
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Permitir HTTP');


    new ec2.Instance(this, 'MyInstance', {
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.genericLinux({ 'us-east-1': 'ami-049d6539112c3246e' }),
      vpc,
      keyName: 'vockey',
      securityGroup: securityGroup,
    });
  }
}

const app = new cdk.App();
new MyEc2Stack(app, 'MyEc2Stack', {
  env: { account: '522813847784', region: 'us-east-1' },
});
