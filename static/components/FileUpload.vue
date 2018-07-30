<template>
    <div>
        <input type="file" @change="read_file" v-if="source === null"/>
        <pre>{{ source }}</pre>
    </div>
</template>

<script>
    const data = {
        source: null,
    }

    export default {
        props: {},

        data: function () {
            return data
        },

        methods: {
            read_file(event) {
                const file = event.target.files[0]
                const self = this
                if (!file) {
                    return
                }
                const reader = new FileReader()
                reader.onload = function (e) {
                    data.source = JSON.parse(e.target.result)
                    self.$emit('file_uploaded', data.source)
                }
                reader.readAsText(file)
            }
        }
    }

</script>
