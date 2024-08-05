#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CdkCustomStack } from '../lib/cdk-custom-stack';

const app = new cdk.App();
new CdkCustomStack(app, 'cdk_custom');
