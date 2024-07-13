let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address_line'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address_line').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}


$(document).ready(function() {
    
    //add cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        var id = $(this).attr("data-id");
        var url = $(this).attr("data-url");
        var data = {
            foodId : id,
        };
        $.ajax({
            url:url,
            method:'GET',
            data:data,
            success : function(response){
                console.log(response)
                console.log(id)
                $('#cart_counter').html(response.cartItem.cartCout);
                $('#qty-'+id).html(response.qty);

                $('#subtotal').html(response.totals.subtotal);
                $('#total').html(response.totals.grand_total);
            }
        })
        
    })

    // decrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        var id = $(this).attr("data-id");
        var url = $(this).attr("data-url");
        var data = {
            foodId : id,
        };
        $.ajax({
            url:url,
            method:'GET',
            data:data,
            success : function(response){
                console.log(response)
                console.log(id)
                $('#cart_counter').html(response.cartItem.cartCout);
                $('#qty-'+id).html(response.qty);


                $('#subtotal').html(response.totals.subtotal);
                $('#total').html(response.totals.grand_total);
            }
        })
        
    })

    // delete cart item
    $('.delete_cart').on('click',function(e){
        
        e.preventDefault();
        var id = $(this).attr("data-id");
        var url = $(this).attr("data-url");
        console.log("checkout-item-"+id);
        var data = {
            foodId : id,
        };
        $.ajax({
            url:url,
            method:'GET',
            data:data,
            success : function(response){
                console.log(response)
                document.getElementById("checkout-item-"+id).remove()
                $('#cart_counter').html(response.cartItem.cartCout);
                // check if cart empty
                

                if (response.cartItem.cartCout == 0){
                    document.getElementById("empty-cart").style.display = "block";
                }

                $('#subtotal').html(response.totals.subtotal);
                $('#total').html(response.totals.grand_total);
            }
        })
        
    })
    // console.log(1);
    $('.item_qty').each(function(){
        var id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+id).html(qty)
        // console.log(id)
    })
    // console.log(2);
});