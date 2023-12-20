$(function(){
	$(".closeform").addEventListener("click", () => {
		var dialog=$("dialog");
		  dialog.close();
	});
$('.carousel').carousel();
$('span.myscript').on('click', function () {
  if (window.filesize > 1024*5) {
    alert('max upload size is 5k');
return false;
  }

  $.ajax({
    // Your server script to process the upload
    url: "/lancerscript",
    type: 'get',

    // Form data
    data: {myid: $(this)[0].dataset.id},

    // Tell jQuery not to process data or worry about content-type
    // You *must* include these options!

    // Custom XMLHttpRequest
    success: function (data) {
	    console.log("HEY")
	    console.log(JSON.stringify(data))
	    console.log(JSON.stringify(data.redirect))
	    if (data.redirect){
	    window.location=data.redirect;
	    }else{
	    window.location="/welcome";
	    }
},
    xhr: function () {
      var myXhr = $.ajaxSettings.xhr();
      if (myXhr.upload) {
        // For handling the progress of the upload
        myXhr.upload.addEventListener('progress', function (e) {
          if (e.lengthComputable) {
            $('progress').attr({
              value: e.loaded,
              max: e.total,
            });
          }
        }, false);
      }
      return myXhr;
    }
  });
	return false;
  });

$('form').on('submit', function () {
  if (window.filesize > 1024*5) {
    alert('max upload size is 5k');
return false;
  }
  $.ajax({
    // Your server script to process the upload
    url: $(this).attr("action"),
    type: 'POST',

    // Form data
    data: new FormData($(this)[0]),

    // Tell jQuery not to process data or worry about content-type
    // You *must* include these options!
    cache: false,
    contentType: false,
    processData: false,

    // Custom XMLHttpRequest
    success: function (data) {
	    console.log("HEY")
	    console.log(JSON.stringify(data))
	    console.log(JSON.stringify(data.redirect))
	    if (data.redirect){
	    window.location=data.redirect;
	    }else{
	    window.location="/welcome";
	    }
},
    xhr: function () {
      var myXhr = $.ajaxSettings.xhr();
      if (myXhr.upload) {
        // For handling the progress of the upload
        myXhr.upload.addEventListener('progress', function (e) {
          if (e.lengthComputable) {
            $('progress').attr({
              value: e.loaded,
              max: e.total,
            });
          }
        }, false);
      }
      return myXhr;
    }
  });
	return false;
  });
	$("#jeuartist").change(function(){
		$.ajax({
			url:"/getsongs",
			data:{"id":$(this).val()},
			type:"get",
			success:function(data){
				var field=$("#jeusong");
				field.html("<option>choisir une chanson</option>");
				var songs=data.songs,song;
				for (var i=0;i<songs.length;i++){
					song=songs[i];
					field.append("<option value=\""+song.id+"\">"+song.title+"</option>");
				}
			}
		});
	});
	$("#jeusong").change(function(){
		$.ajax({
			url:"/getlyrics",
			data:{"id":$(this).val()},
			type:"get",
			success:function(data){
				var field=$("#jeulyric");
				field.html("<option>choisir des paroles</option>");
				var songs=data.lyrics,song;
				for (var i=0;i<songs.length;i++){
					song=songs[i];
					field.append("<option value=\""+song.id+"\">"+song.text+"</option>");
				}
			}
		});
	});
	/*if ($("#choisischanson").length > 0){
	    $("#choisischanson").change(function(){
	    	$.ajax({
	    		url:"/joueraujeu",
	    		data:{"jeu_id": $(this)[0].dataset.jeuId,"song_id":$(this).val()},
	    		type:"get",
	    		success:function(data){
	    			var x= data.redirect;
	    			if (x){
	    				window.location=x;
	    			}
	    		}
	    	});
	    });
        }*/

  
});
