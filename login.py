from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from database import do_database

#dit is een verandering