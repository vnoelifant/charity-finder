$.ajax({
    url: '/heat_map',//url of the function, this should be set in urls.py
    dataType: 'json',
    jsonpCallback: 'getJson',
    beforeSend: function() {
      $('#loader').show();
    },
    success: function(response) {
      $('#loader').hide();
      if (checked && heat == null){
        heat = L.heatLayer(response.map_remaining, {
            radius: 25,
            blur: 25,
            gradient: {
              0.47: 'blue', 
              0.67: 'lime',
              1.0: 'red'
            }
        }).addTo(map);
      }else if (checked){
        map.addLayer(heat)
      }
    }
  })