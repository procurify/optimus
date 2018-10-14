import {debounce, forOwn, omitBy} from 'lodash';

// From https://stackoverflow.com/a/6248722
const generate_uid = function () {
    let firstPart = (Math.random() * 46656) | 0;
    let secondPart = (Math.random() * 46656) | 0;
    firstPart = ('000' + firstPart.toString(36)).slice(-3);
    secondPart = ('000' + secondPart.toString(36)).slice(-3);
    return firstPart + secondPart;
}


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
            if (typeof arr[0] === 'object') {
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

        if (value.type === 'object') {
            result = findObjectByID(value.properties, id)
        } else if (value.type === 'array') {
            result = findObjectByID(value.items.properties, id)
        }
    }

    return result
}


const createObjectByID = function (schema, id) {
    let result = {}
    const keys = Object.keys(schema)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        const value = schema[key]

        if (value.id === id) {
            console.log(schema, value, id)
            // const new_field = 'new_field'
            // result.properties[new_field] = {
            //     id: generate_uid(),
            //     source: new_field,
            //     type: 'string'
            // }
        }

        result[key] = value

        if (value.type === 'object') {
            value.properties = deleteObjectByID(value.properties, id)
            result[key] = value
        } else if (value.type === 'array') {
            value.items.properties = deleteObjectByID(value.items.properties, id)
            result[key] = value
        }
    }

    return result
}


const deleteObjectByID = function (schema, id) {
    let result = {}
    const keys = Object.keys(schema)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        const value = schema[key]

        if (value.id !== id) {
            result[key] = value

            if (value.type === 'object') {
                value.properties = deleteObjectByID(value.properties, id)
                result[key] = value
            } else if (value.type === 'array') {
                value.items.properties = deleteObjectByID(value.items.properties, id)
                result[key] = value
            }
        }
    }

    return result
}


const redrawSchema = function (local_schema) {
    const result = {}
    const keys = Object.keys(local_schema)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        const value = local_schema[key]

        if (value.type === 'object') {
            value.properties = redrawSchema(value.properties)
        } else if (value.type === 'array') {
            value.items.properties = redrawSchema(value.items.properties)
        }

        if ('key' in value) {
            result[value.key] = value
        } else {
            result[key] = value
        }

    }

    return result
}


export {
    schemaGenerator,
    findObjectByID,
    redrawSchema,
    deleteObjectByID,
    createObjectByID
}
