from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from database import do_database
#test