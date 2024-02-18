from setuptools import setup

setup(
    name='disc_bot',
    version='2.0.0',
    entry_points={
        'console_scripts': ['hello-world=hello_world:main'],
        'hello_world.output' : [
            'default=hello_world:default_output'
            ],
        'disc_bot.translator' : [
            'default=lib.translator:Translator'
            ]

    }
)
