#!/usr/bin/env python3

import aws_cdk as cdk
from message_processor.stack import MessageProcessorStack

app = cdk.App()
MessageProcessorStack(app, "MessageProcessorStack")
app.synth()
