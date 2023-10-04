import shared3p;
import shared3p_string;
import stdlib;

import analytics_common;
import common;

domain pd_shared3p shared3p;


template<domain D : shared3p>
DataFrame matToDf(D float32[[2]] mat) {
    DataFrame df = dataFrameNew();
    for (uint i=0; i<shape(mat)[1]; i++) {
        df = dataFrameAddColumn(df, "agg." + tostring(i), mat[:, i]);
    }

    return df;
}

template<domain D : shared3p>
void fedWAvg(D uint proxy, uint nclients, uint nlayers, string ds) {
    string layerName;
    string clientName;
    string tableName;
    DataFrame df;

    for (uint i=0; i<nlayers; i++) {
        if (i < 10) layerName = "layer-0" + tostring(i);
        else layerName = "layer-" + tostring(i);
        D float32[[2]] sumMat;
        for (uint j=0; j<nclients; j++) {
            clientName = "client" + tostring(j+1);
            tableName = clientName + "." + layerName;
            
            // Load the table(layer)
            ResultMat<D> res = loadLayer(proxy, ds, tableName);

            // Check the status
            if (res.status.failed) {
                print("Err. No " + tableName + " table.");
                assert(false);
            }

            // Just sum up. Weights are already weighted according to the data size.
            if (j==0) sumMat = res.mat;
            else sumMat += res.mat;
        }

        // Convert a matrix to DataFrame
        df = matToDf(sumMat);

        // Save
        Status status = dataFrameStore(df, ds, "agg." + layerName, true, proxy);
        
        // Check the status
        if (status.failed) {
            print("Err. Failed in saving 'agg." + layerName);
            assert(false);
        }

        print("agg." + layerName + " has been saved!");
    }
}


void main() {
    pd_shared3p uint proxy;
    
    // Read given arguments
    uint nlayers = argument("nlayers");
    uint nclients = argument("nclients");
    print("num_layers: ", nlayers, ", num_clients: ", nclients);
    
    fedWAvg(proxy, nclients, nlayers, "DS1");

}