from flask import request, Flask, url_for, redirect, render_template
import main
# import exchange_rates
import os
import test
from sqlalchemy import extract
import notification
from exchange_rates import main as exchange
from flask_restful import Resource, Api
from database_management import Offer, Token, Token_Value_Usd
from database_management import main as db_starter
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
# from .getter import getter

from app import app, api

# app = Flask(__name__)
# api = Api(app)

# class Query(Resource):
    # def get(self):
        # return getter.consulta(), 200


class Test(Resource):
    def get(self):
        return test.main(), 200

class Test_msj(Resource):
    def get(self):
        return notification.test('chupame bien la verga tom'), 200
        



def sensor():
    main.filter_db()
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
# sched.add_job(db_starter)
# sched.add_job(sensor)
# sched.add_job(exchange)
sched.add_job(sensor,'interval',minutes=15)
sched.add_job(exchange, 'interval', minutes=60)
sched.start()




# Create routes
# api.add_resource(Query, '/query')
api.add_resource(Test, '/test')
api.add_resource(Test_msj, '/test_msj')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
@app.route('/')
def home():
    return render_template('view_db_table.html', tables=Offer.query.with_entities(Offer.offer_id,
                                                                         Offer.user_name,
                                                                         Offer.finish_rate,
                                                                         Offer.methods,
                                                                         Offer.max_single_trans_amount,
                                                                         Offer.available,
                                                                         Offer.price).\
                                                                        filter(extract('day',Offer.date)==date.today().day).\
                                                                        filter(extract('month',Offer.date)==date.today().month).\
                                                                        filter(extract('year', Offer.date) == date.today().year).all())
@app.route("/cotizaciones")
def cotizaciones():
    return render_template('view_db_coti.html', tables=Token_Value_Usd.query.with_entities(Token_Value_Usd.value_id,
                                                                         Token_Value_Usd.date,
                                                                         Token_Value_Usd.value_usd,
                                                                         Token_Value_Usd.token_id).\
                                                                        filter(extract('day',Offer.date)==date.today().day).\
                                                                        filter(extract('month',Offer.date)==date.today().month).\
                                                                        filter(extract('year', Offer.date) == date.today().year).all())





@app.route('/ultima_notificacion')
def ultima_notificacion():
    with open('falopa.html') as file:
        retv=file.read()
    return retv


# Run the application
if __name__ == '__main__':
    port= int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


