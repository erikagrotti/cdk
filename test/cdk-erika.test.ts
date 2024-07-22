#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CdkErikaStack } from '../lib/cdk-erika-stack';

const app = new cdk.App();
new CdkErikaStack(app, 'cdk_erika');
