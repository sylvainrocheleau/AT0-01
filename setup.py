# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name="project",
    version="1.0",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = scrapy_playwright_ato.settings"]},
    # scripts = ['scripts/generate_cookies.py'],
)
