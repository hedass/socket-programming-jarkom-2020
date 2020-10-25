import epicbox

LIMITS = {'cputime': 64, 'memory': 256}

PROFILES = {
    'python': {
        'docker_image': 'python:3.8-slim',
        'read_only': True,
    },
    'java_compile': {
        'docker_image': 'openjdk:11-jdk-slim',
    },
    'java_run': {
        'docker_image': 'openjdk:11-jdk-slim',
        'read_only': True,
    },
}


def run(code, lang):
    epicbox.configure(profiles=PROFILES)

    with epicbox.working_directory() as workdir:

        if lang == 'python':
            result = epicbox.run(
                'python',
                'python3 main.py',
                files=[{
                    'name': 'main.py',
                    'content': code
                }],
                limits=LIMITS,
                workdir=workdir,
            )

        elif lang == 'text/x-java':
            compile_result = epicbox.run(
                'java_compile',
                'javac Main.java',
                files=[{
                    'name': 'Main.java',
                    'content': code
                }],
                limits=LIMITS,
                workdir=workdir,
            )
            if compile_result['exit_code'] != 0:
                return compile_result
            else:
                result = epicbox.run(
                    'java_run',
                    'java Main',
                    files=[{
                        'name': 'Main.java',
                        'content': code
                    }],
                    limits=LIMITS,
                    workdir=workdir,
                )

        else:
            return 'FATAL: Language Unsupported'

        return result
