import os
import yaml
import io

for region in ['AFRD', 'AFRE', 'SEARD']:
    base_path = "%s/OpenHealthAlgorithms/color_charts/%s" % (os.path.dirname(os.path.realpath(__file__)), region)

    data = {
        'cholesterol': {
            'diabetes': {
                'female': {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
                'male':  {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
            },
            'no_diabetes': {
                'female': {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
                'male':  {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
            },
        },
        'no_cholesterol': {
            'diabetes': {
                'female': {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
                'male':  {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
            },
            'no_diabetes': {
                'female': {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
                'male':  {'smoker': {40: [], 50: [], 60: [], 70: []}, 'non_smoker': {40: [], 50: [], 60: [], 70: []}},
            },
        },
    }
    for file in os.listdir(base_path):
        names = file.split('_')

        var1 = 'cholesterol' if names[0] == 'c' else 'no_cholesterol'
        var2 = 'diabetes' if names[1] == 'd' else 'no_diabetes'
        var3 = 'female' if names[2] == 'f' else 'male'
        var4 = 'smoker' if names[3] == 's' else 'non_smoker'
        var5 = int(names[4].split('.')[0])

        print(var1, var2, var3, var4, var5)

        f = open("%s/%s" % (base_path, file))
        val = []
        if var1 == 'cholesterol':
            for line in f.readlines():
                val_i = []
                for v in line.strip().split(','):
                    val_i.append(int(v))
                val.append(val_i)
        if var1 == 'no_cholesterol':
            for line in f.readlines():
                val.append(int(line.strip()))

        data[var1][var2][var3][var4][var5] = val

    with io.open('%s.yaml' % base_path, 'w+', encoding='utf8') as outfile:
        yaml.dump(data, outfile)
