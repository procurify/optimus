<template>
    <pre>{{ transformed }}</pre>
</template>

<script>
    import {debounce} from 'lodash';

    const data = {
        transformed: null,
    }

    export default {
        props: {
            source: Object,
            schema: Object
        },
        data: function () {
            return data
        },
        computed: {},
        watch: {
            schema: debounce(function (new_value, old_value) {
                const xhr = new XMLHttpRequest();
                xhr.open("POST", 'http://localhost:5000/transform/', true);
                xhr.setRequestHeader("Content-type", "application/json");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        data.transformed = JSON.parse(this.response)
                    }
                }
                xhr.send(JSON.stringify({
                    "input_json": this.source,
                    "schema": new_value
                }))
            }, 1000)
        }
    }
</script>

<style scoped>

</style>
