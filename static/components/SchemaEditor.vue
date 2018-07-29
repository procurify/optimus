<template>
        <pre contenteditable="true"
             v-html="schema"
             v-on:input="update_schema"></pre>
</template>

<script>
    import {debounce} from 'lodash';


    const schema_generator = (function (source) {
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
                schema.type = get_type(json)
                schema.source = key
            }
        }

        parse(source, schema)
        return schema
    })

    const data = {
        schema: null,
    }

    export default {
        props: {
            source: Object
        },
        data: function () {
            return data
        },
        methods: {
            update_schema: debounce(function (event) {
                data.schema = JSON.parse(event.target.innerText)
                this.$emit('schema_generated', data.schema)
            }, 1000)
        },
        watch: {
            source: function (new_value, old_value) {
                data.schema = schema_generator(new_value)
                this.$emit('schema_generated', data.schema)
            }
        }
    }
</script>

<style scoped>

</style>
