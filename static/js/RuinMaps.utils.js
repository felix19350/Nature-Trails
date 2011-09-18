/**
* Requires the help component (UiHelper.utils.js)
* Requires the Detail view component (UiPlaceView.utils.js)
*/

function RuinMaps(debug){
	this.debug = debug === undefined ? false : debug
	this.lat = 38.706946;
	this.lon = -9.14;
	this.addMode = false;
	this.map = null;
	this.uiHelper = new UiHelper();
	if(debug){
		alert("ok");
	}
}

RuinMaps.prototype.toggleAddMode = function(){
	this.addMode = !this.addMode;
	if(this.addMode){
		this.uiHelper.showAddModeOnMsg();
	}else{
		this.uiHelper.showAddModeOffMsg();
	}
};

RuinMaps.prototype.getLatLng = function(){
	return new google.maps.LatLng(this.lat, this.lon);
};

RuinMaps.prototype.createNewLocation = function(formId){
	var self = this;
	var title = $("#title").val();
	var cat = $("#category").val();
	var desc = $("#description").val();
	var links = ""; 
	var linkArr = [];
	$("input[name='link']").each(function(){
		var val = $(this).val();
		if(links.length > 0){
			links += ",";
		}
		links += val;
		linkArr.push(val);
	});
	
	
	var success = function(entry){
		self.addMarker(entry);
		self.uiHelper.showCreateMsg();
	};
	
	var error = function(){
		self.uiHelper.showCreateFailMsg();
	};
	
	var vars = {'latitude': this.lat, 'longitude': this.lon, 'description': desc, 'category': cat, 'title': title, 'links': links};
	this.submitFormTo(formId, vars, success, error);
};

RuinMaps.prototype.addMarker = function(entry){
	var position = new google.maps.LatLng(entry.lat, entry.lon);
	var self = this;
	var marker = new google.maps.Marker({
		position: position,
		title: entry.title
	});
	marker.setMap(this.map);
	marker.setIcon("http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png");
	//Adds event listener for the click in the place mark
	google.maps.event.addListener(marker, 'click', function() {
		var tabOpts = {'container': 'font-size: 12px; padding: 5px; position:fixed; top:60px; right: 0; z-index:998; background-color: white; width: 300px;";'};		
		var tab = new DetailsTab(entry, marker, tabOpts, "parentTab");
		tab.open();
	});
	
	//Drag event
	google.maps.event.addListener(marker, 'dragend', function(){
		var position = marker.getPosition();
		var vars = {'key': entry.key, 'category': entry.category, 'title': entry.title, 'description': entry.description, 'latitude': position.lat(), 'longitude': position.lng(), 'links': entry.links};
		self._submitFormViaPost("/point/update", vars, function(){ self.uiHelper.showUpdateMsg(); }, function(){ self.uiHelper.showUpdateFailMsg(); });
	});
};

RuinMaps.prototype.submitFormTo = function(formId, vars, successHandler, errorHandler){
	var $form = $("#"+formId);
	var dest = $form.attr("action");
	var method = $form.attr("method");

	if(method == "get"){
		this._submitFormViaGet(dest, vars, successHandler, errorHandler)
	}else{
		this._submitFormViaPost(dest, vars, successHandler, errorHandler)
	}
};

RuinMaps.prototype._submitFormViaGet = function(dest, vars, successHandler, errorHandler){
	$.ajax({
		url: dest,
		type: 'GET',
		data: vars,
		success: function(data){
			successHandler(data);
		},
		error: function(){
			errorHandler();	
		}
	});
};

RuinMaps.prototype._submitFormViaPost = function(dest, vars, successHandler, errorHandler){
	$.ajax({
		url: dest,
		type: 'POST',
		data: vars,
		success: function(data){
			successHandler(data);
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			errorHandler();	
		}
	});
};