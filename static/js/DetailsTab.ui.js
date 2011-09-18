/**
 * Creates the dialog/window that show information about a placemark.
 * */
function DetailsTab(entry, marker, styleOpts, parent, closeHandle){
	this.entry = entry;
	this.marker = marker;
	this.uiHelper = new UiHelper();
	this.$parent = parent === null || parent === undefined ? $("body") : $("#"+parent);
	this.styleOpts = styleOpts;
	var self = this;
	
	this.tabId = "detailsTabId" + this.entry.key;
	this.infoContainer = "infoContainer" + this.entry.key;
	this.editFormContainer = "editFormContainer" + this.entry.key;
	this.editFormId = "editPlaceForm" + this.entry.key;
	this.closeBtnId = "closeBtn" + this.entry.key;
	this.editBtnId = "editBtn" + this.entry.key;
	this.pinBtnId = "pinBtn" + this.entry.key;
}

DetailsTab.prototype.open = function(){
	this.$parent.empty();
	var container = "<div id='"+this.tabId+"' style='"+this.styleOpts.container+"display:hidden;' class='ui-corner-all'>";
	container += this._createToolbar();
	container += this._createInfo();
	container += this._createEditForm();
	container += this._createFooter();
	container += "</div>";
	
	this.$parent.append(container);
	$("#"+this.tabId).draggable({disabled: true, addClasses: false});
	this._loadData();
};

DetailsTab.prototype.close = function(){
	this._animateOut();	
};


/**
 * Content creation
 * */

DetailsTab.prototype._createToolbar = function(){
	return "<div style='background-color: #aaa; font-size:10px; padding: 3px;' class='ui-corner-all'><div id='"+this.editBtnId+"' style='float: left;'>Edit</div><div id='"+this.closeBtnId+"' style='float: right;'>Close</div><div style='clear:both;'></div></div>";
};

DetailsTab.prototype._createInfo = function(){
	var length = this.entry.links.length;
	
	var str = "<div id='"+this.infoContainer+"'><p>Title: "+this.entry.title+"</p><p>Category: "+this.entry.category+"</p><p>Description: "+this.entry.description+"</p><hr/>";
	
	if(length > 0){
		str += "<ul>";
		for(var i = 0; i < length; i++){
			str += "<li><a href='"+this.entry.links[i]+"'>"+this.entry.links[i]+"</a></li>";
		}
		str += "</ul>";
	}
	
	str += "</div>";
	return str;
};

DetailsTab.prototype._createEditForm = function(){
	return "<div id='"+this.editFormContainer+"'><p>Title: <input type='text' name='title' value='"+this.entry.title+"'/></p>" +
			"<p>Category"+this._createCategorySelect()+"</p>" +
			"<p>Description<textarea name='description'>"+this.entry.description+"</textarea></div></p>";
};

DetailsTab.prototype._createCategorySelect = function(){
	return "<select name='category'><option value='house'>House</option>" +
					"<option value='palace'>Palace</option>" +
					"<option value='religious'>Religious</option>" + 
					"<option value='industrial'>Industrial</option>" + 
					"<option value='military'>Military</option>" + 
					"<option value='ancient'>Ancient</option></select>";
};

DetailsTab.prototype._createFooter = function(){
	return "<div style='background-color: #aaa; font-size:10px; padding: 3px;' class='ui-corner-all'><div id='"+this.pinBtnId+"' style='float: left;'>Un-Pin</div><div style='clear:both;'></div></div>";	
};

/**
 * Methods that hide & show spot data.
 * */
DetailsTab.prototype._showInfo = function(){
	$("#"+this.infoContainer).show();
};

DetailsTab.prototype._hideInfo = function(){
	$("#"+this.infoContainer).hide();
};

DetailsTab.prototype._showEditForm = function(){
	$("#"+this.editFormContainer).show();	
};

DetailsTab.prototype._hideEditForm = function(){
	$("#"+this.editFormContainer).hide();
};


/**
 * Animates the tab onto the screen.
 * */
DetailsTab.prototype._animateIn = function(){
	var $tab = $("#"+this.tabId);
	var width = $tab.width();
	$tab.width(0);
	
	$tab.animate({"width": width+"px"}, "slow", function(){
		$tab.fadeIn("fast");
	});	
};


/**
 * Collapses the tab out of the screen.
 * */
DetailsTab.prototype._animateOut = function(handler){
	var $tab = $("#"+this.tabId);
	$tab.fadeOut("fast", function(){
		$tab.animate({"width": "0px"}, "slow", function(){
			$tab.remove();	
		});	
	});
};

/**
 * Loads the tab's data.
 * */
DetailsTab.prototype._loadData = function(){
	var self = this;
	this._animateIn();
	this._hideEditForm();
	//TODO: EDIT BUTTON SHOULD HAVE A TOGLE LIKE BEHAVIOUR
	$("#"+this.editBtnId).button({icons: {primary: "ui-icon-pencil"}}).click(function(){
		self.uiHelper.showEditPlaceMsg();
		self.marker.setIcon("http://maps.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png");
		self.marker.setDraggable(true);
		self._hideInfo();
		self._showEditForm();
	});
	
	$("#"+this.closeBtnId).button({icons: {primary: "ui-icon-close"}}).click(function(){
		self.marker.setIcon("http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png");
		self.marker.setDraggable(false);
		self.close();
	});
	$("#"+this.pinBtnId).button({icons: {primary: "ui-icon-pin-w"}}).toggle(
		function(){
			$("#"+self.tabId).draggable("enable");
			$(this).button("option", {icons:{primary:'ui-icon-pin-s'}, label: "Pin"});
		},
		function(){
			$("#"+self.tabId).draggable("disable").removeClass("ui-draggable-disabled ui-state-disabled");
			$(this).button("option", {icons:{primary:'ui-icon-pin-w'}, label: "Un-Pin"});	
		}
	);
}
