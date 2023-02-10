

from flask import Blueprint , render_template, redirect, url_for, request, abort, flash

from app.userinfo.forms import EmptyForm


import stripe

# make @userinfo work from userinfo folder in this file 
payment = Blueprint('payment', __name__)

# todo turn into a database
products = {
    'donations': 
    {
        'name': 'Donation for the site',
        'price': 500, # 500 is = 5.00 , how do I use a counter? Answer turn into a table in a database
    }
}





@payment.route('/donations', methods = ['POST', 'GET'])
def donations():
   

    
    flash(products)
    

    form = EmptyForm()    
    return render_template('stripe_payment/donations.html', products=products, form=form, title='donations')
    '''products = None
    
    if form.validate_on_submit():
        products = products
        # redirect( url_for(userinfo.order, id)) # use once setup database
    '''     


    
'''
    
                <!--- use once database created in donations.html
                <form method="POST" action="/order/{{ id }}">
                    {{ form.csrf_token }}
                    {% set min {{ "$%.2f"|format(products[id].price / 100) }} USD %}
                    <label for="donations">counter:</label>
                    <input type="number" id="donations" name="donations"
                    {{ min }}     max="10000000000000000000000000">
                    {% if products[id].per %}per {{ products[id].per }}{% endif %}                 

 '''

 

@payment.route('/order/<product_id>', methods=['POST'])
def order(product_id):
    # if the prpduct does not exist get a 404 error
    if product_id not in products:
      # create abort page  abort(404)
    # for now use 
       abort(404)
    
    '''
    you can only purchase one product at a time, but since line_items is a list, 
    you can select and buy multiple products if you add a shopping cart interface
    ''' 

    checkout_session = stripe.checkout.Session.create(
        # The line_items  argument specifies the product that the user wishes to buy.
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': products[product_id]['name'],
                    },
                    'unit_amount': products[product_id]['price'],
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],
        # payment_method_types argument allows what payment you want/allow
        payment_method_types=['card'],
        # mode specifies what type of payment you want. An example is payment is a one time payment. 
        mode='payment',
        # stripe will redirect to one of these pages upon the form completion. How?
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)


@payment.route('/order/success')
def success():
    return render_template('success.html')


@payment.route('/order/cancel')
def cancel():
    return render_template('cancel.html')


