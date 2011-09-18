/**
 * Requires the jNotify plugin
 * */

function UiHelper(){
	//var options = {
	//				classContainer: "jnotify-bottom"
	//			  };
	//$.jnotify.setup(options);
}

UiHelper.prototype.showAddModeOnMsg = function(){
	$.jnotify("Double click/tap anywhere on the map to add a new spot.", 5000);
};

UiHelper.prototype.showAddModeOffMsg = function(){
	$.jnotify("Leaving edition mode.", 5000);
};

UiHelper.prototype.showEditPlaceMsg = function(){
	$.jnotify("Drag the selected placemark in order to change the position.", 5000);	
};

UiHelper.prototype.showCreateMsg = function(){
	$.jnotify("Location created.", 5000);	
};

UiHelper.prototype.showCreateFailMsg = function(){
	$.jnotify("Error creating position.", 5000);	
};

UiHelper.prototype.showUpdateMsg = function(){
	$.jnotify("Location updated.", 5000);	
};

UiHelper.prototype.showUpdateFailMsg = function(){
	$.jnotify("Error updating location.", 5000);	
};

