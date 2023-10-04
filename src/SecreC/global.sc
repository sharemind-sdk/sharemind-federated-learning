import shared3p;
import stdlib;

import analytics_common;
import common;

domain pd_shared3p shared3p;

void main() {
    pd_shared3p uint proxy;
    uint nlayers = argument("nlayers");
    print("num_layers: ", nlayers);

    string layerName;
    string tableName;
    DataFrame df;

    for (uint i=0; i<nlayers; i++) {
        if (i < 10) layerName = "layer-0" + tostring(i);
        else layerName = "layer-" + tostring(i);
        tableName = "agg." + layerName;
        
        // Load the table(layer)
        ResultMat<pd_shared3p> res = loadLayer(proxy, "DS1", tableName);

        // Check the status
        if (res.status.failed) {
            print("Err. Failed in loading the " + tableName + " table.");
            assert(false);
        }

        publish(layerName, res.mat);
    }
}