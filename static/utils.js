import {debounce} from 'lodash';

const schemaGenerator = function (source) {
    const schema = {}

    const supported_types = [
        'string', 'number', 'array', 'object',
        'boolean', 'integer', 'function', 'tuple'
    ];

    function is_plain_object(obj) {
        return obj ? typeof obj === 'object'
            && Object.getPrototypeOf(obj) === Object.prototype : false;
    }

    function generate_uid() {
        // From https://stackoverflow.com/a/6248722
        let firstPart = (Math.random() * 46656) | 0;
        let secondPart = (Math.random() * 46656) | 0;
        firstPart = ("000" + firstPart.toString(36)).slice(-3);
        secondPart = ("000" + secondPart.toString(36)).slice(-3);
        return firstPart + secondPart;
    }

    function get_type(type) {
        if (!type) type = 'string';
        if (supported_types.indexOf(type) !== -1) {
            return type;
        }
        return typeof type;
    }

    function is_schema(object) {
        return supported_types.indexOf(object.type) !== -1
    }

    function handle_schema(json, schema) {
        Object.assign(schema, json);

        if (schema.type === 'object') {
            delete schema.properties;
            parse(json.properties, schema);
        }
        if (schema.type === 'array') {
            delete schema.items;
            schema.items = {};
            parse(json.items, schema.items)
        }
    }

    function handle_array(arr, schema, key) {
        schema.id = generate_uid()
        schema.type = 'tuple'
        schema.source = key + '[*]'
        if (arr.length > 0) {
            if (typeof arr[0] === "object") {
                schema.type = 'array'
                let props = schema.items = {}
                parse(arr[0], props)
            }
        }
    }

    function handle_object(json, schema, key) {
        if (is_schema(json)) {
            return handle_schema(json, schema)
        }
        schema.id = generate_uid()
        schema.type = 'object';
        schema.required = [];
        let props = schema.properties = {};
        for (let key in json) {
            const item = json[key];
            let curSchema = props[key] = {};
            if (key[0] === '*') {
                delete props[key];
                key = key.substr(1);
                schema.required.push(key);
                curSchema = props[key] = {};
            }
            curSchema.source = key
            parse(item, curSchema, key)
        }
    }

    function parse(json, schema, key) {
        if (Array.isArray(json)) {
            handle_array(json, schema, key)
        } else if (is_plain_object(json)) {
            handle_object(json, schema, key)
            if (schema.required !== undefined && schema.required.length === 0) {
                delete schema.required
            }
        } else {
            schema.id = generate_uid()
            schema.type = get_type(json)
            schema.source = key
        }
    }

    parse(source, schema)
    return schema
}

const json_formatter = (function (source) {
    const NUM_TYPE = 'number'
    const STR_TYPE = 'string'
    const BOOL_TYPE = 'boolean'
    const ARR_TYPE = 'array'
    const OBJ_TYPE = 'object'

    const get_type = function (data) {
        const data_type = typeof data
        if (data_type === OBJ_TYPE) {
            if (Array.isArray(data_type)) {
                return ARR_TYPE
            }
            return OBJ_TYPE
        }
        return data_type
    }

    const iterate = function (data) {
        let output = ''
        const data_type = get_type(data)

        console.log(data_type)

        if (data_type === ARR_TYPE) {
            output += '<ul>'
            for (let item of data) {
                output += iterate(item)
            }
            output += '</ul>'
        } else if (data_type === OBJ_TYPE) {
            output += '<ul>'
            for (const [key, value] of Object.entries(data)) {
                const _data_type = get_type(value)
                if (_data_type === ARR_TYPE || _data_type === OBJ_TYPE) {
                    output += `<li>${key} ${iterate(value)}</li>`
                } else {
                    output += iterate(`${key}: ${value}`)
                }
            }
            output += '</ul>'
        }

        output += `<li>${data}</li>`
        return output
    }

    return iterate(source)
})


const findObjectByID = function (schema, id) {
    let result = null
    const keys = Object.keys(schema)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        const value = schema[key]

        if (value.id === id) {
            value.key = key
            result = value
        }

        if (result !== null) break

        if (value.type === "object") {
            result = findObjectByID(value.properties, id)
        } else if (value.type === "array") {
            result = findObjectByID(value.items.properties, id)
        }

    }

    return result
}

const redrawSchema = function (local_schema) {
    const keys = Object.keys(local_schema)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        const value = local_schema[key]

        if ('key' in value) {
            delete local_schema[key]
            local_schema[value.key] = value
        }

        if (value.type === "object") {
            redrawSchema(value.properties)
        } else if (value.type === "array") {
            redrawSchema(value.items.properties)
        }

    }
}


export {
    schemaGenerator,
    findObjectByID,
    redrawSchema
}
