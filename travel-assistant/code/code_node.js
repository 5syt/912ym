async function main(args) {
    const params = args.params;

    const ret = {
        records: [
            {
                fields: {
                    "用户问题": params["user"],
                    "Bot回复": params["bot"],
                    "是否FAQ": "否"
                }
            }
        ]
    };

    return ret;
}
