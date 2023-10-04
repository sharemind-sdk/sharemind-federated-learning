import shared3p;
import shared3p_string;
import stdlib;

import analytics_common;

template<domain D : shared3p>
struct ResultMat {
    D float32[[2]] mat;   // even though, it's vector, saved as a matrix.
    Status status;
}


template<domain D : shared3p>
ResultMat<D> loadLayer(D uint proxy, string ds, string tbl) {
    Result res = dataFrameRead(ds, tbl, proxy);

    public ResultMat<D> result;
    result.status = res.status;

    if (result.status.failed) {
        return result;
    }

    DataFrame df = getDataFromResult(res);
    result.mat = dataFrameGetMatrix(df);

    dataFrameDelete(df);
    return result;
}

uint strToUint(uint8[[1]] num) {
    uint result = 0;
    uint multipler = 1;
    uint len = size(num);
    for (uint i=0; i<len; i++) {
        result += ((uint)(num[len-i-1] - 48)) * multipler;
        multipler *= 10;
    }
    return result;
}

template<domain D : shared3p>
uint stringToUint(string s, D uint proxy) {
    D xor_uint8[[1]] bl_s = bl_str(s);
    uint8 [[1]] _s = declassify(bl_s);
    return strToUint(_s);
}