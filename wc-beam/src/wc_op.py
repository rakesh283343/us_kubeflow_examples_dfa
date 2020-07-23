#!/usr/bin/env python3
import kfp
from kfp import dsl


def wc_op(input_path: str, output_path: str):
    return dsl.ContainerOp(
        name='Apache Beam - Direct Training',
        image='localhost:5005/examples-word-count',
        arguments=[
            '--input', input_path,
            '--output', output_path,
        ]
    )