from setuptools import setup, find_packages


VERSION = '0.0.3'
DESC = 'My DWM runner'


setup(
    name='bendwm',
    url='https://github.com/benwah/bendwm',
    author='Benoit C. Sirois',
    author_email='benoitcsirois@gmail.com',
    version='0.0.2',
    description=DESC,
    long_description=DESC,
    packages=find_packages(),
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Window Managers',
    ],
    install_requires=[
        'pydwm',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'bendwm = bendwm:start',
        ]
    }
)
