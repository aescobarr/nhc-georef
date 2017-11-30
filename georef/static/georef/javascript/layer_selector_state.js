var LayerSelector = function(json){
    if(json){
        this.json = JSON.parse(json);
    }else{
        this.json = {
            base : "",
            overlays: []
        };
    }

    this.setBase(base){
        this.json.base = base;
    }

    this.getBase(){
        return this.json.base;
    }

    this.setOverlays(array){
        this.json.overlays = array;
    }

    this.getOverlays(){
        return this.json.overlays;
    }
}

var getEstatSelectorFormatJSON(selector){

}