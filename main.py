import click
from src.suppressor import AudioSuppressor

@click.command()
@click.option('--input', '-i', required=True, help='Input audio file')
@click.option('--output', '-o', required=True, help='Output audio file')
@click.option('--noise-reduction', '-nr', default=0.7, help='Noise reduction strength (0.0-1.0)')

def main(input, output, noise_reduction):
    suppressor = AudioSuppressor()
    suppressor.reduce_noise(input, output, noise_reduction)
    click.echo(f'Successfully processed: {input} -> {output}')

if __name__ == '__main__':
    main()
