import ml
import common as cm

if __name__ == "__main__":
    model = ml.get_model()

    # Check the weights
    weight_shape = [w.shape for w in model.get_weights()]
    model_shape = "|".join([",".join(map(str, tup)) for tup in weight_shape])

    # Write out this model structure
    with open(f"{cm.PROJECT_PATH}/client/model.txt", 'w') as f:
        f.write(model_shape)

    print("/client/model.txt hes been created.")
