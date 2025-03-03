import * as ddb from '@aws-appsync/utils/dynamodb'

export function request(ctx) {
	return ddb.get({ key: { id: ctx.args.id, sk: ctx.args.sk } })
}

export const response = (ctx) => ctx.result