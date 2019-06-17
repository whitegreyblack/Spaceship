@echo off
REM python -m tests.test_components
REM pytest tests\test_components.py

REM ecs components
python -m ecs.components.component
python -m ecs.components.position
python -m ecs.components.health
python -m ecs.components.experience
python -m ecs.components.render
python -m ecs.components.information
