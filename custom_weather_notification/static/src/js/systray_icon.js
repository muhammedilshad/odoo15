/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var ExampleWidget = Widget.extend({
   template: 'Systray_weather',
   events: {
       'click #create_so': '_onClick',
   },
   _onClick: function(){
    function location(position){
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var api_key = 'f4d2cd2ad92ec1ce690dafa6e4cfadf4';
    $.getJSON('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + '&appid=' + api_key, function(data){
    var place = data.name
    var pressure = data.main.pressure
    var climate_desc = data.weather[0].description
    var climate = data.weather[0].main
    var celsius = data.main.temp - 273.15
    var rounded_celsius = Math.round(celsius).toFixed(2)
    var today_date = $.datepicker.formatDate('dd/mm/yy', new Date());
    swal({
        title: "Weather Now",
        text: '    '+ today_date +'\n\n'+ rounded_celsius +'°   '+ climate +'\n\n'+ climate_desc +' in ' + place +'\n\n'+'Near  '+ place,
        button: "Ok",
    });
    })
    }
   if ('geolocation' in navigator){
  navigator.geolocation.getCurrentPosition(location);
   }}
});
SystrayMenu.Items.push(ExampleWidget);
export default ExampleWidget;