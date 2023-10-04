import shared3p;
import shared3p_string;
import shared3p_random;
import stdlib;

import analytics_common;
import common;

domain pd_shared3p shared3p;


template<domain D : shared3p>
void publishString(D uint proxy, string key, string value) {
    D xor_uint8[[1]] message = bl_str(value);
    publish(key, (uint8) message);
}

template<type T>
uint getIndex(T[[1]] vec, T val) {
    for (uint i=0; i<size(vec); i++) {
        if (vec[i] == val) return i;
    }

    assert(false);
    return 0;
}

template<domain D : shared3p>
uint[[2]] constructModelShape(D xor_uint8[[1]] bl_model) {
    /*
     * Key ASCII:
     *  - 44 -> ,
     *  - 124 -> |

     * The weight shape is up to 4D.
     */
    D uint proxy;
    // This is not credential
    uint8[[1]] model = declassify(bl_model);

    // Count the "|"
    uint nrow = sum(model == 124) + 1;

    uint[[2]] result(nrow, 4);
    uint8[[1]] chunk;
    uint k;
    uint l;
    bool contain_comma;
    for (uint i=0; i<nrow; i++) {
        for (uint j=0; j<size(model); j++) {
            if (model[j] == 124) {
                chunk = model[:j];   // represents one layer
                model = model[j+1:]; // rest of the layers
                break;
            }
            chunk = model;
        }
        contain_comma = any(chunk == 44);
        if (contain_comma) {
            l = 0;
            k = getIndex(chunk, 44u8);
            result[i, l] = strToUint(chunk[:k]);
            contain_comma = any(chunk[k+1:] == 44);
            chunk = chunk[k+1:];
            while (contain_comma) {
                l += 1;
                k = getIndex(chunk, 44u8);
                result[i, l] = strToUint(chunk[:k]);
                chunk = chunk[k+1:];
                contain_comma = any(chunk == 44);
            }
            result[i, l+1] = strToUint(chunk);
        } else {
            result[i, 0] = strToUint(chunk);
        }
    }

    return result;
}


template<domain D : shared3p, type T>
T[[1]] randomUniform(D uint proxy, uint M, T lim_below, T lim_upper) {
    D uint[[1]] seed(M);
    D T[[1]] uniform_dist = (T) randomize(seed) / (T) UINT64_MAX;

    // Scale up to the limits
    uniform_dist *= lim_upper - lim_below;

    // Shift according to the limit
    return declassify(uniform_dist + lim_below);
}

template<domain D : shared3p, type T>
T[[2]] randomUniform(D uint proxy, uint nrow, uint ncol, T lim_below, T lim_upper) {
    T[[2]] result(nrow, ncol);
    for (uint i=0; i<nrow; i++) result[i, :] = randomUniform(proxy, ncol, lim_below, lim_upper);

    return result;
}

template<domain D : shared3p, type T>
T[[1]] glorotUniform(D uint proxy, uint[[1]] _shape) {
    // Default method in keras
    T lim = sqrt(6 / (T)(sum(_shape)));
    
    uint nnode = _shape[0] * _shape[1];  // 2D
    if (_shape[2] != 0) nnode = nnode * _shape[2] * _shape[3]; // 4D
    return randomUniform(proxy, nnode, -lim, lim);
}

template<domain D : shared3p>
void createInitModel(D uint proxy, uint[[2]] model_shape, string ds) {
    assert(shape(model_shape)[1] == 4);
    uint nrow = shape(model_shape)[0];
    float32[[1]] weight;     // even if a layer is not 1D, Sharemind handles it as flatten vector.
    D float32[[1]] _weight;
    string name;
    bool dense_before = false;

    // TODO: probably there is a better way for initializing batch normalization layer
    bool bn_1 = true;    // all ones
    bool bn_2 = false;   // all zeros
    bool bn_3 = false;   // all zeros
    bool bn_4 = false;   // all ones

    for (uint i=0; i<nrow; i++) {
        if (i < 10) name = "layer-0" + tostring(i);
        else name = "layer-" + tostring(i);
        DataFrame df = dataFrameNew();
        ResultMat<D> res = loadLayer(proxy, ds, "init." + name);

        if (res.status.failed) {
            if (model_shape[i, 1] == 0){
                if (dense_before) {
                    // init bias to 0
                    float32[[1]] bias(model_shape[i, 0]);
                    D float32[[1]] _bias = bias;
                    publish(name, bias);
                    print(model_shape[i, 0]);

                    df = dataFrameAddColumn(df, name, _bias);
                    dense_before = false;
                } else {
                    // Batch normalization layer
                    float32[[1]] bias(model_shape[i, 0]);
                    if (bn_1) {
                        bias = 1;
                        bn_1 = false;
                        bn_2 = true;
                    } else if (bn_2) {
                        bias = 0;
                        bn_2 = false;
                        bn_3 = true;
                    } else if (bn_3) {
                        bias = 0;
                        bn_3 = false;
                        bn_4 = true;
                    } else {
                        bias = 1;
                        bn_4 = false;
                        bn_1 = true;
                    }
                    D float32[[1]] _bias = bias;
                    publish(name, bias);
                    print(model_shape[i, 0]);

                    df = dataFrameAddColumn(df, name, _bias);
                }
            } else {
                weight = glorotUniform(proxy, model_shape[i, :]);
                _weight = weight; 
                dense_before = true;

                publish(name, weight);
                print(size(weight));

                df = dataFrameAddColumn(df, name, _weight);
            }

            // Save
            Status status = dataFrameStore(df, ds, "init." + name, true, proxy);
        } else { // meaning it's already created before
            publish(name, res.mat);
            print(shape(res.mat)[0]);
        }
    }
}


void main() {
    // Construct the model shape defined.
    string model = argument("model");
    pd_shared3p xor_uint8[[1]] bl_model = bl_str(model);
    uint[[2]] model_shape = constructModelShape(bl_model);
    print("Layers' shapes:");
    printMatrix(model_shape);

    pd_shared3p uint proxy;
    createInitModel(proxy, model_shape, "DS1");

}