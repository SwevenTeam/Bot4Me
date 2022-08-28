
const validateApiKey = new RegExp(
    '^\\d{8}-\\d{4}-\\d{4}-\\d{4}-\\d{12}$', 'gm'
 );

export default validateApiKey