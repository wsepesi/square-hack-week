import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function test() {
    // fetch the api route "api/test/{string}" and get the data
    const { data, error, isLoading } = useSWR('/api/test/Helloworld', fetcher)

    if (error) return <div>Failed to load</div>
    if (isLoading) return <div>Loading...</div>
    if (!data) return null

    return (
        <div>
            <h1>{data}</h1>
        </div>
    )
}