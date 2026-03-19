import h5py
import json

def fix_config(config):
    if isinstance(config, dict):
        if 'batch_shape' in config:
            batch_shape = config.pop('batch_shape')
            config['input_shape'] = batch_shape[1:]
        for key in ['optional', 'quantization_config', 'synchronized']:
            config.pop(key, None)
        if 'dtype' in config:
            dtype_val = config['dtype']
            if isinstance(dtype_val, dict) and dtype_val.get('class_name') == 'DTypePolicy':
                config['dtype'] = dtype_val['config']['name']
        for value in list(config.values()):
            fix_config(value)
    elif isinstance(config, list):
        for item in config:
            fix_config(item)

with h5py.File("model/soil_model.h5", "r+") as f:
    model_config = f.attrs.get("model_config")
    if model_config:
        config = json.loads(model_config)
        fix_config(config)
        f.attrs["model_config"] = json.dumps(config)
        print("Fixed!")

    # Also fix layer configs inside the file
    def fix_group(group):
        for key in group.keys():
            item = group[key]
            if hasattr(item, 'attrs'):
                for attr_key in item.attrs:
                    try:
                        val = json.loads(item.attrs[attr_key])
                        fix_config(val)
                        item.attrs[attr_key] = json.dumps(val)
                    except:
                        pass
            if hasattr(item, 'keys'):
                fix_group(item)

    fix_group(f)
    print("All layers fixed!")