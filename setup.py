from setuptools import setup, find_packages

setup(name='minGPT',
      version='0.0.1',
      author='Andrej Karpathy',
      packages=find_packages(),
      description='A PyTorch re-implementation of GPT with Credible PDF Signature Scanner',
      license='MIT',
      install_requires=[
            'torch',
            'pdf2image>=3.1.0',
            'pytesseract>=0.3.10', 
            'opencv-python>=4.5.0',
            'pandas>=1.3.0',
            'Pillow>=8.0.0',
            'openpyxl>=3.0.0',
      ],
      extras_require={
            'transformers': ['transformers>=4.0.0'],
      },
      entry_points={
            'console_scripts': [
                  'credible-scanner=credible_scanner_cli:main',
            ],
      },
)
