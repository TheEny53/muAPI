sap.ui.define([
	"sap/ui/core/mvc/Controller"
], function (Controller) {
	"use strict";

	return Controller.extend("sap.ui.demo.walkthrough.controller.ArtistList", {


	/* 	onInit: function () {
			var oModel = new sap.ui.model.json.JSONModel();
			var aData = jQuery.ajax({
				type: "GET",
				contentType: "application/json",
				url: "https://mu-api.herokuapp.com/api/v1/artists", 
				dataType: "json", 
				success: function(data, textStatus, jqXHR){
					var oData = {
						"artists": data
					}
					oModel.setData(oData);
				}
				
		});
		this.getView().setModel(oModel);

	} */
}
)});